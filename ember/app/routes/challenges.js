import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('authController', this.controllerFor('auth'));
    controller.set('ctf', this.controllerFor('application').get('ctf'));
    controller.set('user', this.controllerFor('application').get('user'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },
});
