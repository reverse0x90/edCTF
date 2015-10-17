import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('ctf', this.controllerFor('application').get('ctf'));
  },
});
