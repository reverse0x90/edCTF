import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    var t = this;
    return this.store.find('ctf', 1);
  },
  setupController: function (controller, model){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('ctfs', model);
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },
});
