# Personal Workflow Notes


The Unreasonable Effectiveness Of Plain Text
https://www.youtube.com/watch?v=WgV6M1LyfNY

## Commit often

Git is a time machine. You you can go back and forward and explore other timelines. It's just obtuse and interrupts my workflow so I don't commit enougn.

I need automatic commits that don't just generage garbage.

###

Text based todo workflow....

One central branch.... main?... production?... active?

A list of todos:

You indicate you're working on one somehow.
A watcher sees the change and creates a new banch for the todo.

Work work work on the thing you're doing.

Every time you hit 'run'. A new 'squashable' commit is created.

When you're done with a task you run a task which squashs the feature branch and creates a merge (or pull request) with the text of the todo item as message.

Also:
Maybe don't commit if builds are failing

Also: Maybe you tag it with a code to trigger it and tive it a feature name:

Todos.md:

- [ ] #ORP-1234 Fix the blah blah blah
