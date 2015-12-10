import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('session', this.controllerFor('auth').get('session'));
    controller.set('ctf', this.controllerFor('application').get('ctf'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('settings', this.controllerFor('admin').get('settings'));
  },
});
