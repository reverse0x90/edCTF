import Ember from 'ember';

export default Ember.Route.extend({
  foo: 'foo',
  authcontroller: null,
  setupController: function (controller, model){
    controller.set('foo', this.get('foo'));
    controller.set('authcontroller', this.controllerFor('auth'));
   
  },

});
