const express = require('express');
const path = require('path');
const port = process.env.PORT;
const app = express();
const history = require('connect-history-api-fallback')
const https = require('https');
const http = require('http');
const compression = require('compression');
const server = http.createServer(/** … **/);
const serveStatic = require('serve-static');
const GracefulShutdownManager = require('@moebius/http-graceful-shutdown').GracefulShutdownManager;
const fs = require('mz/fs');
const httpShutdownManager = new GracefulShutdownManager(server);

process.on('SIGTERM', () => {
	httpsShutdownManager.terminate(() => {
		httpShutdownManager.terminate(() => {
			console.log('Server is gracefully terminated');
		});
	});
});

app.use(compression());

async function start(){

  app.use(history({
    verbose: true
  }))

  // async function getCerts(){
  //   const certdir = (await fs.readdir("/etc/letsencrypt/live"))[1];
  //   return {
  //     key: await fs.readFile(`/etc/letsencrypt/live/${certdir}/privkey.pem`),
  //     cert: await fs.readFile(`/etc/letsencrypt/live/${certdir}/fullchain.pem`)
  //   }
  // }
  
  // const {key, cert} = await getCerts()
  
  // the __dirname is the current directory from where the script is running
  app.use(serveStatic(path.join(__dirname, './build'), { 
    maxAge: 30*60*60*24*1000,
    setHeaders: setCustomCacheControl
  }));

  // send the user to index html page inspite of the url
  app.get('*', (req, res) => {
    res.sendfile(path.resolve(__dirname, './build/index.html'));
  });

const httpApp = express();

httpApp.get('*', function(req, res) {
  // console.log('tenenemos', req.headers.host + req.url)
  // res.redirect('https://' + req.headers.host + req.url);
  // console.log(req.headers.host + req.url,'redirecting')
  res.sendfile(path.resolve(__dirname, './build/index.html'));
})
const httpServer = http.createServer(httpApp).listen(80);
//https.createServer({key, cert}, app).listen(443)
}

function setCustomCacheControl (res, path) {
  if (serveStatic.mime.lookup(path) === 'text/html') {
    // Custom Cache-Control for HTML files
    res.setHeader('Cache-Control', 'public, max-age=0')
  }
}

start()