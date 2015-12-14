import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    return this.store.findAll('ctf');
  },
  setupController: function (controller, model){
    controller.set('model', model);
    controller.set('session', this.controllerFor('auth').get('session'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('appController', this.controllerFor('application'));
  },
});
