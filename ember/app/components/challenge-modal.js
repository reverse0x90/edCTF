import Ember from 'ember';

export default Ember.Component.extend({
  challenge: {},
  modal: {},
  flag: '',
  correctFlagMsg: '',
  wrongFlagMsg: '',
  errorMessage: '',
  errorFields:{},
  classNames: ['challenge-submit', 'challenge-cancel'],
  validatorController: undefined,
  user: {},
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isChallenge', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setupFocus: function() {
      Ember.$('#inputFlag').focus();
  }.on('didInsertElement'),
  checkServer: function(flag) {
    var t = this;
    var data = {'flag': flag};
    var challenge_id = t.get('challenge.id');
    var namespace = t.get('store').adapterFor('application').namespace;

    Ember.$.post(namespace+'/challenges/'+challenge_id, data, function(data){
      if(data.success){
        t.set('correctFlagMsg', 'Congratulations you have the correct flag!');
        t.set('wrongFlagMsg', '');
        t.set('modal.solvedChallenge', challenge_id);
      } else {
        t.set('wrongFlagMsg', 'Sorry wrong flag');
        t.set('correctFlagMsg', '');
      }
    }).error(function() {
      t.set('wrongFlagMsg', 'Something went wrong');
      t.set('correctFlagMsg', '');
    });
  },
  actions: {
    closeChallengeModal: function() {
      this.set('modal.isChallenge', false);
    },
    submitFlag: function() {
      var t = this;
      var validator = this.get('validatorController');
      var flag = t.get('flag');

      // If flag is not valid show error message on form
      if ( !validator.isvalidFlag(flag) ) {
        t.set('errorMessage', validator.get('error'));
        t.set('errorFields', validator.get('errorFields'));
      }
      // Else flag is valid send the flag to the server to check if it is correct
      else{
        t.set('errorMessage', '');
        t.set('errorFields', {});
        t.checkServer(flag);
        // Blank out flag value
        t.set('flag', '');
      }

      // Make sure to refocus after flag has been submitted
      Ember.$('#inputFlag').focus();
    },
  }
});

