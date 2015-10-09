import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    return this.store.findAll('challenge');
  },
  setupcontroller: function(controller, model){
    controller.set('model', model);
    controller.set('challenges', model);
  }

});
