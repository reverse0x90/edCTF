import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    return this.store.findAll('challenge');
  },
  setupController: function (controller, model){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('challenges', model);
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },
});
