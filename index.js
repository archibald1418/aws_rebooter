import {PythonShell} from 'python-shell';
import 'dotenv/config'; // load .env variables
const {exec} = await import('child_process');

const handler = (err, stdout, stderr) => {
  if (err) {
    console.error(err);
  } else {
    console.log(stdout);
  }
};

// exec('which python', handler);
// exec(`source aws_tg/bin/activate`, handler)
// exec('which python', handler);

const options = {
  mode : "text",
  pythonPath: './aws_tg/bin/python3',
  pythonOptions: ['-u'],
  // args
  // scriptPath
};


let shell = new PythonShell('main.py', options)  

// Capture python's stdout 
shell.on('message', function(message) {
  console.log(message)
});



shell.end( (err, conde, signal) => {
  if (err)
    throw err;
  console.log(err)
  console.log('Code = ${code}, signal = ${signal}');
});



//shell.run().then(messages=>{
//  console.log('results: %j', messages);
//}); // array of messages collected during execution
//
