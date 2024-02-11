import {PythonShell} from 'python-shell';
import 'dotenv/config'; // load .env variables
const {exec} = await import('child_process');


// PythonShell.runString('x=1+1;print(x)', null).then(messages=>{
//   console.log('finished');
// });

exec('which python', (err, stdout, stderr) => {
  if (err) {
    console.error(err);
  } else {
  console.log(stdout);
  }
});

const options = {
  mode : "text",
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
