import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  viewTeam: true,
  teamname: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  scoreboardController: null,
  store: null,
  challenges: [],
  challengeSorting: ['timestamp:desc'],
  sortedChallenges: Ember.computed.sort('challenges', 'challengeSorting'),
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isRegister', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setChallenges: function(){
    if(!this.get('modal.adminCtf')){
      return;
    }

    var challengeTimestamps = this.get('modal.adminTeam.solves');
    var store = this.get('store');
    if(challengeTimestamps){
      var t = this;
      this.get('modal.adminCtf.challengeboard').then(function(){
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
  }.observes('modal.adminTeam').on('init'),
  actions: {
    toggleView: function(){
      this.toggleProperty('viewTeam');
    },
    closeAdminTeamModal: function() {
      this.set('modal.isAdminTeam', false);
      this.set('modal.adminCtf', null);
      this.set('modal.adminScoreboard', null);
      this.set('modal.adminTeam', null);
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});
    },
    createTeam: function() {
      var team = {
        scoreboard: this.get('modal.adminScoreboard'),
        teamname: this.get('teamname'),
        username: this.get('username'),
        email: this.get('email'),
        password: this.get('password'),
        confirmPassword: this.get('confirmPassword'),
      };
      this.get('scoreboardController').send('createTeam', team);
    },
    editTeam: function(){
      this.get('scoreboardController').send('editTeam', this.get('modal.adminTeam'), this.get('password'), this.get('confirmPassword'));
    },
    deleteTeam: function(){
      this.get('scoreboardController').send('deleteTeam', this.get('modal.adminTeam'));
    },
  },
});
