import Ember from 'ember';

export default Ember.Route.extend({
  setupController: function (controller){
    controller.set('ctf', this.controllerFor('application').get('ctf'));
  },
});
