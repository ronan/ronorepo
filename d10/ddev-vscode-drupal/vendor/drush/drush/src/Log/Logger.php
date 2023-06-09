<?php

declare(strict_types=1);

namespace Drush\Log;

use Drush\Drush;
use Robo\Log\RoboLogger;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * Contains \Drush\Log\Logger.
 *
 * This is the actual Logger for Drush that is responsible
 * for logging messages.
 *
 * This logger is designed such that it can be provided to
 * other libraries that log to a Psr\Log\LoggerInterface.
 *
 * Those who may wish to change the way logging works in Drush
 * should therefore NOT attempt to replace this logger with their
 * own LoggerInterface, as it will not work.  It would be okay
 * to extend Drush\Log\Logger, or perhaps we could provide a way
 * to set an output I/O object here, in case output redirection
 * was the only thing that needed to be swapped out.
 */
class Logger extends RoboLogger
{
    public function __construct(OutputInterface $output)
    {
        parent::__construct($output);
    }

    public function log($level, $message, array $context = []): void
    {
        // Append timer and memory values.
        if (Drush::debug()) {
            $timer = round(microtime(true) - (int) $_SERVER['REQUEST_TIME'], 2);
            $suffix = sprintf(' [%s sec, %s]', $timer, self::formatSize(memory_get_usage()));
            $message .= $suffix;
        }

        // consolidation/log handles formatting and verbosity level check.
        parent::log($level, $message, $context);
    }

    // Copy of format_size() in Drupal.
    public static function formatSize($size)
    {
        if ($size < DRUSH_KILOBYTE) {
            // format_plural() not always available.
            return dt('@count bytes', ['@count' => $size]);
        } else {
            $size /= DRUSH_KILOBYTE; // Convert bytes to kilobytes.
            $units = [
                dt('@size KB'),
                dt('@size MB'),
                dt('@size GB'),
                dt('@size TB'),
                dt('@size PB'),
                dt('@size EB'),
                dt('@size ZB'),
                dt('@size YB'),
            ];
            foreach ($units as $unit) {
                if (round($size, 2) >= DRUSH_KILOBYTE) {
                    $size /= DRUSH_KILOBYTE;
                } else {
                    break;
                }
            }
            return str_replace('@size', (string) round($size, 2), $unit);
        }
    }
}
