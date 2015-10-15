import Ember from 'ember';

export default Ember.Route.extend({
  beforeModel: function(transition){
    this.authCheck(transition);
    //will have other stuff here once its connected to restapi
  },
  authCheck: function(transition){
    //Method to check user credentials and redirect if necessary
    console.log('Checking authentication');
    var t = this;
    var auth = t.controllerFor('auth');
    var modal = t.controllerFor('modal');
    console.log("targetName in application route: ", transition.targetName);
    if (!auth.inwhiteList(transition.targetName)) {
      if(!auth.isAuthenticated){
        auth.set('currentTransition', transition);
        transition.abort();
        console.log('User is unauthenicated, opening login modal');
        modal.set('modal.isLogin', true);  
        t.transitionTo('index');
      }
    }
  },
  setupController: function (controller, model){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },  
  actions: {
    willTransition: function(transition){
      this.authCheck(transition);
    }
  }
});