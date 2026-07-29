const { spawn } = require('child_process');

const npmCommand = 'npm';

const processes = [];

function startProcess(name, command) {
  const child = spawn(command, {
    stdio: 'inherit',
    shell: true,
  });

  child.on('exit', (code, signal) => {
    if (signal || code !== 0) {
      shutdown(signal || `exit code ${code}`);
    }
  });

  processes.push({ name, child });
}

function shutdown(reason) {
  for (const { child } of processes) {
    if (!child.killed) {
      child.kill();
    }
  }

  if (reason) {
    console.log(`Stopping dev servers (${reason})`);
  }

  process.exit(0);
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

startProcess('backend', `${npmCommand} run dev --prefix backend`);
startProcess('frontend', `${npmCommand} run dev --prefix frontend`);