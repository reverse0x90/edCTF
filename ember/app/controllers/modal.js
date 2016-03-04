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
    adminCtf: null,
    adminCategory: null,
    adminChallenge: null,
    adminScoreboard: null,
    adminTeam: null,
    solvedChallenge: -1,
    errorMessage: '',
    errorFields: {},
  },
  store: null,
});
