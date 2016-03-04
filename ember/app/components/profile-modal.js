import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  session: {},
  team: {},
  password: '',
  confirmPassword: '',
  viewProfile: true,
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isProfile', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setTeam: function(){
    var team = this.get('session').team;
    if(team){
      var t = this;
      team.then(function(team){
        var username = t.get('session').username;
        var email = t.get('session').email;
        if (username){
          team.set('username', username);
        }
        if (email){
          team.set('email', email);
        }
        t.set('team', team);
      });
    }
  }.observes('session').on('init'),
  challenges: [],
  store: undefined,
  challengeSorting: ['timestamp:desc'],
  sortedChallenges: Ember.computed.sort('challenges', 'challengeSorting'),
  setChallenges: function(){
    var challengeTimestamps = this.get('team.solves');
    var store = this.get('store');

    if(challengeTimestamps){
      var t = this;
      this.get('ctf.challengeboard').then(function(){
        var challenges = [];

        for (var i = 0; i < challengeTimestamps.length; i++) {
          var id = challengeTimestamps[i][0];
          var time = new Date(challengeTimestamps[i][1] * 1000);
          var foundChallenge = store.peekRecord('challenge', id);

          if(foundChallenge){
            var foundCategory = store.peekRecord('category', foundChallenge.get('category').id);
            if(foundCategory){
              var challenge = {
                title: foundChallenge.get('title'),
                points: foundChallenge.get('points'),
                category: foundCategory.get('name'),
                timestamp: time.toUTCString().replace(' GMT','')
              };
              challenges.push(challenge);
            }
          }
        }
        challenges = Ember.A(challenges);
        t.set('challenges', challenges);
      });
    }
  }.observes('team').on('init'),
  actions: {
    toggleView: function(){
      this.toggleProperty('viewProfile');
    },
    closeProfileModal: function() {
      this.set('modal.isProfile', false);
    },
    editProfile: function(){
      this.sendAction('editProfile', this.get('session'), this.get('password'), this.get('confirmPassword'));
    },
  },
});
