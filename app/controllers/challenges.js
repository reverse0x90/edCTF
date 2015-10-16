import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  challenge: {},
  challenges: null,
  sortedChallenges: function() {
    return Ember.ArrayProxy.extend(Ember.SortableMixin).create({
      sortProperties: ['category', 'points'],
      sortAscending: true,
      content: this.get('challenges')
    });
  }.property('challenges'),
  uniqueCategories: function () {
    var uniqueCategories = [];
    var category = '';
    this.get('challenges').forEach(function(item) {
      category = item.get('category');
      if (uniqueCategories.indexOf(category) === -1 ) {
        uniqueCategories.push(category);
      }
    });
    return uniqueCategories.sort();
  }.property('challenges'),
  actions: {
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openChallenge: function(id) {
      this.store.find('challenge', id).then((challenge) => {
        this.set('modal.challenge', challenge);
      });
      this.set('modal.isChallenge', true);
    },
  }
});