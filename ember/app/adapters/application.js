import DS from 'ember-data';
import Ember from 'ember';

export default DS.RESTAdapter.extend({
  namespace: 'api',
  headers: Ember.computed(function(){
    var token = Ember.$.cookie('csrftoken');
    return {'X-CSRFToken': token};
  }),
});