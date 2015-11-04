/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'ed-ctf',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },
    contentSecurityPolicy: {
      'default-src': "'self' 'unsafe-eval' https://www.google.com/ http://*.googleapis.com/ https://*.googleapis.com/",
      'script-src': "'self' 'unsafe-eval' https://www.google.com/ http://*.googleapis.com/ https://*.googleapis.com/",
      'font-src': "'self' 'unsafe-eval' https://www.google.com/ http://*.gstatic.com/ http://*.googleapis.com/ https://*.googleapis.com/",
      'connect-src': "'self' 'unsafe-eval' https://www.google.com/ http://*.googleapis.com/ https://*.googleapis.com/",
      'img-src': "'self' 'unsafe-eval' http: https:",
      'style-src': "'self' 'unsafe-eval' 'unsafe-inline' https://www.google.com/ http://*.googleapis.com/ https://*.googleapis.com/", 
      'media-src': "'self' 'unsafe-eval' https://www.google.com/ http://*.googleapis.com/ https://*.googleapis.com/",
    },
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
