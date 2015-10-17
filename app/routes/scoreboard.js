import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('modal', this.controllerFor('modal').get('modal'));
    controller.set('scoreboard', this.controllerFor('application').get('ctf.scoreboard'));
  },
});
