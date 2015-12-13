import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('session', this.controllerFor('auth').get('session'));
    controller.set('ctfController', this.controllerFor('admin.ctf'));
    controller.set('challengeboardController', this.controllerFor('admin.challengeboard'));
    controller.set('scoreboardController', this.controllerFor('admin.scoreboard'));
    controller.set('teamsController', this.controllerFor('admin.teams'));
  },
});
