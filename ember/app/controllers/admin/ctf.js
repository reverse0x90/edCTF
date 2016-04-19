import Ember from 'ember';

export default Ember.Controller.extend({
  model: null,
  modal: {},
  host: window.location.origin,
  appController: null,
  editCtfName: '',
  editCtfOnline: false,
  errorMessage: '',
  errorFields: {},
  modalErrorMessage: '',
  modalErrorFields: {},
  ctfSorting: ['online:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  selectedCtf: null,
  selectedOption: {
    'view': true,
    'edit': false,
  },
  setSelectedCtf: function(){
    this.set('selectedCtf', this.get('appController').get('ctf'));
  }.observes('appController.ctf'),
  actions: {
    promptConfirmation: function(messageArray, callback){
      this.set('modal.confirmMesg', messageArray);
      this.set('modal.confirmCallback', callback);
      this.set('modal.isConfirm', true);
    },
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
    changeSelectedCtf: function(ctf){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('selectedCtf', ctf);
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setViewOption: function(){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setEditOption: function(){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('editCtfName', this.get('selectedCtf.name'));
      this.set('editCtfOnline', this.get('selectedCtf.online'));
      this.set('selectedOption', {
        'view': false,
        'edit': true,
      });
    },
    createCtfConfirmed: function(name, online){
      var t = this;
      var ctf = this.store.createRecord('ctf', {
        name: name,
        online: online,
      });
      ctf.save().then(function(ctf){
        t.set('modal.isAdminCtf', false);
        t.set('modal.errorMessage', '');
        t.set('modal.errorFields', {});
        if(ctf.get('online')){
          var online_ctf = t.get('appController.ctf');
          if(online_ctf){
            online_ctf.set('online', false);
          }
          t.set('appController.ctf', ctf);
        }
      }, function(err){
        ctf.deleteRecord();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
          t.set('modal.errorFields', err.errors.fields);
        } else {
          t.set('modal.errorMessage', 'Server error');
          t.set('modal.errorFields', {});
        }
      });
    },
    createCtf: function(name, online){
      if(!name){
        this.set('modal.errorMessage', 'Invalid CTF name');
        this.set('modal.errorFields', {'name': true});
        return;
      }
      var t = this;

      // check if name already taken
      this.store.filter('ctf', function(ctf) {
        return ctf.get('name') === name;
      }).then(function(foundCtf) {
        var found = foundCtf.get('length');
        if(found){
          t.set('modal.errorMessage', 'CTF name already taken');
          t.set('modal.errorFields', {'name': true});
        } else {
          if(online){
            var online_ctf = t.get('appController.ctf');
            if(online_ctf){
              t.send('promptConfirmation', [
                'This will replace "' + online_ctf.get('name') + '" as the current online ctf.',
                'Are you sure?',
              ], function(confirmed){
                if(confirmed){
                  t.send('createCtfConfirmed', name, true);
                } else {
                  t.set('modal.errorMessage', '');
                  t.set('modal.errorFields', {});
                }
              });
            } else {
              t.send('createCtfConfirmed', name, true);
            }
          } else {
            t.send('createCtfConfirmed', name, false);
          }
        }
      });
    },
    editCtfConfirmed: function(ctf, new_ctf, callback){
      var t = this;
      ctf.set('name', new_ctf.name);
      ctf.set('online', new_ctf.online);
      ctf.save().then(function(){
        t.set('selectedOption', {
          'view': true,
          'edit': false,
        });
        if(callback){
          callback();
        }
      }, function(err){
        ctf.rollbackAttributes();
        if (err.errors.message){
          t.set('errorMessage', err.errors.message);
          t.set('errorFields', err.errors.fields);
        } else {
          t.set('errorMessage', 'Server error, unable to edit CTF');
          t.set('errorFields', {});
        }
      });
    },
    editCtf: function(){
      var t = this;
      var name = this.get('editCtfName');
      var online = this.get('editCtfOnline');
      var ctf = this.get('selectedCtf');

      if(!name){
        this.set('errorMessage', 'Invalid CTF name');
        this.set('errorFields', {'name': true});
        return;
      }

      // check if name already taken
      this.store.filter('ctf', function(ctf) {
        return ctf.get('name') === name;
      }).then(function(foundCtf) {
        var found = foundCtf.get('length');
        if(found && ctf.get('name') !== name){
          t.set('errorMessage', 'CTF name already taken');
          t.set('errorFields', {'name': true});
        } else {
          t.set('errorMessage', '');
          t.set('errorFields', {});
          if(online === ctf.get('online')){
            t.send('editCtfConfirmed', ctf, {
              'name': name,
              'online': online,
            });
          } else {
            var onlineCtf = t.get('appController').get('ctf');
            if(onlineCtf){
              if(onlineCtf.get('online')){
                if(onlineCtf.get('id') === ctf.get('id')){
                  // onlineCtf is going offline, confirm with user
                  t.send('promptConfirmation', [
                    'This will take the ctf "' + onlineCtf.get('name') + '" offline.',
                    'Are you sure?',
                  ], function(confirmed){
                    if(confirmed){
                      t.send('editCtfConfirmed', ctf, {
                        'name': name,
                        'online': online,
                      }, function(){
                        t.get('appController').set('ctf', undefined);
                      });
                    }
                  });
                } else {
                  if(online){
                    // replacing online ctf, confirm with user
                    t.send('promptConfirmation', [
                      'This will replace "' + onlineCtf.get('name') + '" as the current online CTF.',
                      'Are you sure?',
                    ], function(confirmed){
                      if(confirmed){
                        t.send('editCtfConfirmed', ctf, {
                          'name': name,
                          'online': online,
                        }, function(){
                          t.get('appController').set('ctf', ctf);
                        });
                      }
                    });
                  } else {
                    t.send('editCtfConfirmed', ctf, {
                      'name': name,
                      'online': online,
                    });
                  }
                }
              } else {
                // if onlineCtf isnt online for some reason, just update the ctf
                t.send('editCtfConfirmed', ctf, {
                  'name': name,
                  'online': online,
                });
              }
            } else {
              t.send('editCtfConfirmed', ctf, {
                'name': name,
                'online': online,
              }, function(){
                if(online){
                  t.get('appController').set('ctf', ctf);
                }
              });
            }
          }
        }
      });
    },
    deleteCtf: function(){
      var t = this;
      var ctf = this.get('selectedCtf');

      this.send('promptConfirmation', [
        'This will DELETE the ctf "' + ctf.get('name') + '" and all challenges, scoreboards, and teams associated with it.',
        'Are you REALLY sure?!',
      ], function(confirmed){
        if(confirmed){
          // disallow online ctf deletion
          if(ctf.get('online')){
            t.set('errorMessage', 'Cannot delete a online CTF');
            t.set('errorFields', {});
          } else {
            // DELETE the ctf!
            ctf.deleteRecord();
            ctf.save().then(function(){
              // replace selected ctf with another
              var onlineCtf = t.get('appController').get('ctf');
              if(onlineCtf){
                t.set('selectedCtf', onlineCtf);
              } else {
                var nextCtf = t.get('sortedCtfs');
                if(nextCtf){
                  nextCtf = nextCtf.get('firstObject');
                  if(nextCtf){
                    t.set('selectedCtf', nextCtf);
                  } else {
                    t.set('selectedCtf', undefined);
                  }
                } else {
                  t.set('selectedCtf', undefined);
                }
              }
              
              // set option to view
              t.set('selectedOption', {
                'view': true,
                'edit': false,
              });
            }, function(err){
              ctf.rollbackAttributes();
              if (err.errors.message){
                t.set('errorMessage', err.errors.message);
                t.set('errorFields', err.errors.fields);
              } else {
                t.set('errorMessage', 'Server error, unable to delete CTF');
                t.set('errorFields', {});
              }
            });
          }
        } else {
          t.set('errorMessage', '');
          t.set('errorFields', {});
        }
      });
    },
    openCtfHomeModal: function(){
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});
      this.set('modal.htmlPage', this.get('selectedCtf').get('home'));
      this.set('modal.isAdminHtml', true);
    },
    openCtfAboutModal: function(){
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});
      this.set('modal.htmlPage', this.get('selectedCtf').get('about'));
      this.set('modal.isAdminHtml', true);
    },
  },
});
