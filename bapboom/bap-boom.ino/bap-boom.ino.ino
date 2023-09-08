/*

Blink bright white light from a single Neopixel!

*/
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

#include <MozziGuts.h>
#include <Oscil.h>
#include <ADSR.h>
#include <Ead.h>
#include <mozzi_rand.h>
#include <EventDelay.h>
#include <Metronome.h>


#define PIN_NUM_ROT_L_CLK   12
#define PIN_NUM_ROT_L_DT    27
#define PIN_NUM_ROT_L_SW    33
#define PIN_NUM_ROT_R_CLK   15
#define PIN_NUM_ROT_R_DT    32
#define PIN_NUM_ROT_R_SW    14
#define PIN_NUM_MATRIX      4

#define MATRIX_L            0
#define MATRIX_R            15 
#define MATRIX_T            0
#define MATRIX_B            7

#define NUM_TRACKS          4
#define NUM_STEPS           16

#define TRACKS_T            MATRIX_B - NUM_TRACKS + 1
#define TRACKS_B            MATRIX_B


uint16_t colors[16] = {
  0xF206,
  0xE8EC,
  0x9936,
  0x61D6,
  0x3A96,
  0x24BE,
  0x055E,
  0x05FA,
  0x04B1,
  0x4D6A,
  0x8E09,
  0xCEE7,
  0xFF47,
  0xFE00,
  0xFCC0,
  0xFAA4
};
#define COLOR_BLACK         0x0000
#define COLOR_WHITE         0xFFFF
#define COLOR_SELECT        0xFFFF
#define COLOR_SELECT_Y      0xFFFF
#define COLOR_SELECT_X      0xFFFF
#define COLOR_BG            COLOR_BLACK

uint16_t track_colors[4] = {colors[0], colors[5], colors[10], colors[15]};


Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(
                            16, 8, PIN_NUM_MATRIX,
                            NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
                            NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
                            NEO_GRB            + NEO_KHZ800
                        );


enum {
  PIN_ROT_L_SW = 0,
  PIN_ROT_L_DT,
  PIN_ROT_L_CLK,
  PIN_ROT_R_SW,
  PIN_ROT_R_CLK,
  PIN_ROT_R_DT,
  PIN_COUNT
};

char pin_nums[PIN_COUNT] = {
  PIN_NUM_ROT_L_SW, 
  PIN_NUM_ROT_L_DT, 
  PIN_NUM_ROT_L_CLK,
  PIN_NUM_ROT_R_SW,
  PIN_NUM_ROT_R_CLK,
  PIN_NUM_ROT_R_DT
};

bool pins[PIN_COUNT];
bool pins_prev[PIN_COUNT];
bool pins_delta[PIN_COUNT];

void read_pins() {
  for (int i = 0; i < PIN_COUNT; i++) {
    pins[i]       = digitalRead(pin_nums[i]);
    pins_delta[i] = pins[i] ^ pins_prev[i];
    pins_prev[i]  = pins[i];
  }
}


char pattern[NUM_TRACKS][NUM_STEPS] = {
  {1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0},
  {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
  {0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0},
  {1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0},
  // {1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0},
  // {1,1,0,0,0,1,0,1,1,0,1,1,0,0,0,1},
  // {1,0,1,0,1,0,0,0,1,1,1,1,0,1,1,0},
  // {1,0,0,1,0,0,0,0,0,1,1,0,1,0,1,1},
};

#include <tables/whitenoise8192_int8.h>
#include <tables/brownnoise8192_int8.h>
#include <tables/sin8192_int8.h>
#include <tables/cos8192_int8.h>
#include <tables/saw8192_int8.h>


#define CONTROL_RATE        256 
#define WAVE_TABLE_SIZE     8192

typedef Oscil<WAVE_TABLE_SIZE, AUDIO_RATE>  Oscil8192;
typedef const int8_t*                       wt;

int           tempo         = 8;
int           current_step  = 0;
int           cursor_x      = 0;
int           cursor_y      = 0;


Oscil8192     oscilators[NUM_TRACKS];
Metronome     tick_track(64 + ((16 - tempo) * 16));
Ead           gain_envelopes[NUM_TRACKS] {Ead(CONTROL_RATE), Ead(CONTROL_RATE), Ead(CONTROL_RATE), Ead(CONTROL_RATE)};

typedef struct              { int freq;     int attack;     int decay;      int bend;   int phase;      int level;      wt wave;                } voice;
voice voices[NUM_TRACKS] =  {                 
                            {     5,            2,              6,              8,          0,               3,         SIN8192_DATA            },
                            {     6,            1,              1,              8,          0,               1,         WHITENOISE8192_DATA     },
                            {     7,            2,              6,              8,          0,               4,         BROWNNOISE8192_DATA     },
                            {     1,            2,              10,             8,          0,               10,        COS8192_DATA            },
};

void setup() {
  Serial.begin (115200);

  startMozzi(CONTROL_RATE);
  tick_track.start();  

  for (int i = 0; i < NUM_TRACKS; i++) {
    oscilators[i] = Oscil<WAVE_TABLE_SIZE, AUDIO_RATE>(voices[i].wave);
  }

  matrix.begin();
  matrix.setBrightness(50);

  pinMode(PIN_NUM_ROT_L_CLK, INPUT_PULLUP);
  pinMode(PIN_NUM_ROT_L_DT,  INPUT_PULLUP);
  pinMode(PIN_NUM_ROT_L_SW,  INPUT_PULLUP);
  pinMode(PIN_NUM_ROT_R_CLK, INPUT_PULLUP);
  pinMode(PIN_NUM_ROT_R_DT,  INPUT_PULLUP);
  pinMode(PIN_NUM_ROT_R_SW,  INPUT_PULLUP);
  read_pins();
}

int32_t levels[NUM_TRACKS];

void updateControl() {
  bool refresh_matrix = false;

  read_pins();
  if (pins[PIN_ROT_L_CLK] && pins_delta[PIN_ROT_L_CLK]){     
     if (pins[PIN_ROT_L_DT] != pins[PIN_ROT_L_CLK]) { 
        cursor_y--;
     } else {
        cursor_y++;
     }
     if (cursor_y >= NUM_TRACKS) cursor_y = NUM_TRACKS - 1;
     if (cursor_y < 0) cursor_y = 0;
     refresh_matrix = true;
  }

  if (pins[PIN_ROT_R_CLK] && pins_delta[PIN_ROT_R_CLK]){     
     if (pins[PIN_ROT_R_DT] != pins[PIN_ROT_R_CLK]) { 
        cursor_x--;
     } else {
        cursor_x++;
     }
     if (cursor_x > MATRIX_R) cursor_x = MATRIX_R;
     if (cursor_x < MATRIX_L) cursor_x = MATRIX_L;
     refresh_matrix = true;
  }

  if (pins_delta[PIN_ROT_R_SW] && !pins[PIN_ROT_R_SW]) {
    pattern[cursor_y][cursor_x] = !pattern[cursor_y][cursor_x];
    refresh_matrix = true;
  }

  uint8_t tick = tick_track.ready();
  current_step = (current_step + tick) % NUM_STEPS;

  for (int i = 0; i < NUM_TRACKS; i++) {
    if(tick && pattern[i][current_step]) {
        oscilators[i].setPhase(voices[i].phase * 8);
        oscilators[i].setFreq(voices[i].freq * voices[i].freq * 32);
        gain_envelopes[i].start(voices[i].attack * 8, voices[i].decay * 8);
    }

    levels[i] = (gain_envelopes[i].next() * voices[i].level);
  }


  if (refresh_matrix || tick) {
    matrix.fillScreen(COLOR_BG);
    for (int i = 0; i < 16; i++) {
      matrix.drawPixel(i, 0, colors[i]);
    }

    if (cursor_y >= 0) {
      matrix.drawLine(MATRIX_L, TRACKS_T + cursor_y, MATRIX_R, TRACKS_T + cursor_y, COLOR_SELECT_Y);

      for (int i = 0; i < NUM_TRACKS; i++) {
        for (int j = 0; j < NUM_STEPS; j++) {
          if (pattern[i][j]) {
            matrix.drawPixel(j, TRACKS_T + i, track_colors[i]);
          }
        }
      }
      matrix.drawLine(cursor_x, TRACKS_T, cursor_x, TRACKS_B, COLOR_SELECT_X);
      matrix.drawPixel(cursor_x, TRACKS_T + cursor_y, pattern[cursor_y][cursor_x] ? track_colors[cursor_y] : COLOR_SELECT );
    }
    else {
      matrix.drawPixel(TRACKS_T + cursor_y, 0, COLOR_SELECT);
    }
    matrix.drawPixel(current_step, 3, COLOR_SELECT);
    matrix.show();
  }
}

AudioOutput_t updateAudio(){
  int32_t out = 0;

  for (int i = 0; i < NUM_TRACKS; i++) {
    out += (oscilators[i].next() * levels[i]);
  }
  return out >> 12;
}


void loop() {
  audioHook();
}
