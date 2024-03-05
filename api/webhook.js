module.exports = (request, response) => {
  console.log(request.body)
    response
    .status(200)
    .send(JSON.stringify({
      body: request.body,
      query: request.query,
      cookies: request.cookies
    }, null, 2));
};
