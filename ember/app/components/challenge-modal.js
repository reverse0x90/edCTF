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
  session: {},
  closeModal: function(){
    var t = this;
    return function(callback){
      t.set('flag', '');
      t.set('errorMessage', '');
      t.set('errorFields', {});
      t.set('modal.isChallenge', false);
      if(callback){
        callback();
      }
    };
  }.property('closeModal'),
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.get('closeModal')();
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setupFocus: function() {
      Ember.$('#inputFlag').focus();
  }.on('didInsertElement'),
  actions: {
    closeChallengeModal: function() {
      this.get('closeModal')();
    },
    submitFlag: function() {
      var t = this;
      var validator = this.get('validatorController');
      var flag = this.get('flag');

      // If flag is not valid show error message on form
      if ( !validator.isvalidFlag(flag) ) {
        this.set('errorMessage', validator.get('error'));
        this.set('errorFields', validator.get('errorFields'));
      }
      // Else flag is valid send the flag to the server to check if it is correct
      else{
        var challengeid = this.get('challenge.id');
        this.set('errorMessage', '');
        this.set('errorFields', {});
        //this.submitFlag(flag);
        this.sendAction('submitFlag', challengeid, flag, function(success, error){
          if(success){
            t.set('correctFlagMsg', 'Congratulations you have the correct flag!');
            t.set('wrongFlagMsg', '');
            t.set('modal.solvedChallenge', challengeid);
          } else {
            if (error){
              t.set('wrongFlagMsg', error);
              t.set('correctFlagMsg', '');
            } else {
              t.set('wrongFlagMsg', 'Sorry wrong flag');
              t.set('correctFlagMsg', '');
            }
          }
        });
        // Blank out flag value
        t.set('flag', '');
      }

      // Make sure to refocus after flag has been submitted
      Ember.$('#inputFlag').focus();
    },
  }
});

