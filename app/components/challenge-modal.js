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
    // This function will POST the flag to the server and get the response
    if (flag == 'edCTF') {
      this.set('correctFlagMsg', 'Congratulations you have the correct flag!');
      this.set('wrongFlagMsg', '');
    }
    else {
      this.set('wrongFlagMsg', 'Sorry wrong flag, please try again!');
      this.set('correctFlagMsg', '');
    }
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

