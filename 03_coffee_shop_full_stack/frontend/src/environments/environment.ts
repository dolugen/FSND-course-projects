/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'udacity-coffeeshop.eu', // the auth0 domain prefix
    audience: 'coffeeshop-api', // the audience set for the auth0 app
    clientId: 'SxaeMJ20JeffaV11n10GtGP7fAR8aMAC', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4201', // the base url of the running ionic application. 
  }
};
