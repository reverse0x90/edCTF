import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('appController', this.controllerFor('application'));
    controller.set('scoreboardController', this.controllerFor('scoreboard'));
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('model', this.controllerFor('admin').get('model'));
  },
});
