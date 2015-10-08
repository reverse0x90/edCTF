import Ember from 'ember';

export default Ember.Route.extend({
  model: function(){
    return this.store.find('challenge');
  },
  setupcontroller: function(controller, model){
    controller.set('model', model);
    controller.set('challenges', model);
  }

});
