import Ember from 'ember';

export default Ember.Controller.extend({
  appController: null,
  selectedCtf: null,
  setSelectedCtf: function(){
    this.set('selectedCtf', this.get('appController').get('ctf'));
  }.observes('appController.ctf'),
  selectedChallengeboard: null,
  setSelectedChallengeboard: function(){
    this.set('selectedChallengeboard', this.get('selectedCtf').get('challengeboard'));
  }.observes('selectedCtf'),
});
