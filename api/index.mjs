import { PythonShell } from "python-shell";
import dotenv from "dotenv"; // load .env variables
import express from "express";

dotenv.config({
  path: ".env",
});
const { exec } = await import("child_process");

const handler = (err, stdout, stderr) => {
  if (err) {
    console.error(err);
  } else {
    console.log(stdout);
  }
};

const options = {
  mode: "text",
  pythonPath: process.env.PYTHONPATH,
  pythonOptions: ["-u"], // unbuffered output (allows to intercept python's prints)
  scriptPath: process.env.SCRIPTPATH,
  // args
  // scriptPath
};

function exec_python() {
  let shell = new PythonShell("main.py", options);

  console.log("Python shell created");

  // Capture python's stdout
  shell.on("message", function (message) {
    console.log(`Python: ${message}`);
  });

  shell.end((err, code, signal) => {
    if (err) throw err;
    console.error(err);
    console.log(`Code = ${code}, signal = ${signal}`);
  });
}

/*
 ** Express app ------------------------------------------------------
 */

// const app = express();
// const port = 3001;

// app.get("/", (req, res) => {
//   console.log("Express: i am up");
//   res.send(JSON.stringify({ who: "your mom", status: "gay" }, null, "\t"));
// });

// export default app;
// module.exports = app;

function bootstrap() {
  // app.listen(port, () => console.log(`Express server ready on port ${port}`));
  exec_python();
}

bootstrap();

