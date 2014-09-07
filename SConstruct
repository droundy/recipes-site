import time, os, math

env = Environment(CPPPATH=['.'], LIBS=[])

# Configure git to run the test suite:
Alias('git configuration',
      env.Command(target = '.git/hooks/commit-msg',
                  source = 'git-scripts/commit-msg',
                  action = Copy("$TARGET", "$SOURCE")))
Alias('git configuration',
      env.Command(target = '.git/hooks/pre-commit',
                  source = 'git-scripts/pre-commit',
                  action = Copy("$TARGET", "$SOURCE")))
Default('git configuration')

env.Command(target='doc/.layout/style.css',
            source= ['doc/.layout/style.scss'],
            action = 'sass $SOURCE $TARGET')

env.Command(target='doc/.layout/style.scss',
            source= ['doc/.layout/style.py', 'doc/.layout/responsive.py'],
            action = 'python $SOURCE > $TARGET')
Alias('web', 'doc/.layout/style.css')

web = Environment(tools=['matplotlib', 'mkdown'])
Alias('web', web.Markdown('doc/index.md'))
Default('web')
