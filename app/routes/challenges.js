import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    var t = this;
    return this.store.findAll('ctf');
  },
  setupController: function (controller, model){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('ctfs', model);
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },
});
