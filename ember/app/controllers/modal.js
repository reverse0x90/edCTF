import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {
    isLogin: false,
    isRegister: false,
    isChallenge: false,
    isTeam: false,
    isProfile: false,
    isAdminCtf: false,
    isAdminTeam: false,
    isAdminChallenge: false,
    isConfirm: false,
    confirmMesg: [''],
    confirmCallback: null,
    challenge: {},
    team: {},
    adminCategory: {},
    adminChallenge: {},
    solvedChallenge: -1,
    errorMessage: '',
    errorFields: {},
  },
  store: null,
});
