import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    return this.store.findAll('team');
  },
  setupController: function (controller, model){
    controller.set('teams', model);
    controller.set('modal', this.controllerFor('modal').get('modal'));
  },
});
