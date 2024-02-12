import {PythonShell} from 'python-shell';
import 'dotenv/config'; // load .env variables
import express from 'express';

const {exec} = await import('child_process');

const handler = (err, stdout, stderr) => {
  if (err) {
    console.error(err);
  } else {
    console.log(stdout);
  }
};

const options = {
  mode : "text",
  pythonPath: './aws_tg/bin/python3',
  pythonOptions: ['-u'],
  // args
  // scriptPath
};

function exec_python(){

  let shell = new PythonShell('main.py', options)  

  console.log("Python shell created")

  // Capture python's stdout 
  shell.on('message', function(message) {
    console.log(`Python: ${message}`)
  });

  shell.end( (err, conde, signal) => {
    if (err)
      throw err;
    console.log(err)
    console.log('Code = ${code}, signal = ${signal}');
  });
};

/* 
** Express app ------------------------------------------------------
*/

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  console.log("Express: i am up");
  res.json( {
    who: "your mom",
    status : "gay"
  });
});

function bootstrap()
{
  app.listen(port);
  exec_python();
}

bootstrap()
