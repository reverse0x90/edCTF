import Ember from 'ember';

export default Ember.Route.extend({
  beforeModel: function(transition){
    this.authCheck(transition);
    //will have other stuff here once its connected to restapi
  },
  model: function(){
    return this.store.find('ctf', 1);
  },
  authCheck: function(transition){
    //Method to check user credentials and redirect if necessary
    var t = this;
    var auth = t.controllerFor('auth');
    var modal = t.controllerFor('modal');
    if (!auth.inwhiteList(transition.targetName)) {
      if(!auth.isAuthenticated){
        auth.set('currentTransition', transition);
        transition.abort();
        modal.set('modal.isLogin', true);  
        t.transitionTo('index');
      }
    }
  },
  setupController: function (controller, model){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('ctf', model);
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },  
  actions: {
    willTransition: function(transition){
      this.authCheck(transition);
    }
  }
});