import Ember from 'ember';

export default Ember.Controller.extend({
  appController: null,
  ctfSorting: ['online:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  selectedCtf: null,
  setSelectedCtf: function(){
    this.set('selectedCtf', this.get('appController').get('ctf'));
  }.observes('appController.ctf'),
  selectedChallengeboard: null,
  setSelectedChallengeboard: function(){
    this.set('selectedChallengeboard', this.get('selectedCtf').get('challengeboard'));
  }.observes('selectedCtf'),
  actions: {
    changeSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
    },
    createCategory: function(challengeboard){
      console.log('Opening create category modal, challengeboard:', challengeboard);
    },
    editCategory: function(category){
      console.log('Opening edit category modal, category:', category);
    },
    deleteCategory: function(category){
      console.log('Deleting category, category:', category);
    },
    createChallenge: function(category){
      console.log('Opening create challenge modal, category:', category);
    },
    editChallenge: function(challenge){
      console.log('Opening edit challenge modal, challenge:', challenge);
    },
    deleteChallenge: function(challenge){
      console.log('Deleting challenge, challenge:', challenge);
    },
  },
});
