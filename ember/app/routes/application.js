import Ember from 'ember';

export default Ember.Route.extend({
  beforeModel: function(transition){
    this.authCheck(transition);
    //will have other stuff here once its connected to restapi

    // Forward all request for index to home
    if (transition.targetName === 'index' ){
      this.transitionTo('home');
    }
  },
  model: function(){
    return this.store.query('ctf', {'live': true});
  },
  authCheck: function(transition){
    //Method to check user credentials and redirect if necessary
    var t = this;
    var auth = t.controllerFor('auth');
    var modal = t.controllerFor('modal');
    var application = t.controllerFor('application');

    auth.checkLoggedIn(function(){
      application.set('session', auth.session);
      if(!auth.session.isAuthenticated && auth.inblackList(transition.targetName)){
        auth.set('currentTransition', transition);
        transition.abort();
        modal.set('modal.isLogin', true);  
        t.transitionTo('index');
      }
    });
  },
  setupController: function (controller, model){
    // Get first instance of live ctf
    controller.set('ctf', model.get('firstObject'));
    controller.set('authController', this.controllerFor('auth'));
    controller.set('validatorController', this.controllerFor('validator'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('adminSettings', this.controllerFor('admin').get('settings'));
  },
  actions: {
    willTransition: function(transition){
      this.authCheck(transition);
    }
  },
  afterModel: function(model) {
    Ember.$(document).attr('title', model.get('name'));
  },
});