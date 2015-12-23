import Ember from 'ember';

export default Ember.Controller.extend({
  appController: null,
  isCreatingCategory: false,
  editingCategory: null,
  newCategoryName: '',
  errorMessage: '',
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
  setFocus: function(){
    setTimeout(function(){
      Ember.$('#inputCategory').focus();
    }, 200);
  }.observes('isCreatingCategory', 'editingCategory'),
  init: function(){
    Ember.$('#categoryDelete').click(function() {Ember.$('#categoryDelete').stop();});
  },
  actions: {
    promptConfirmation: function(messageArray, callback){
      this.set('modal.confirmMesg', messageArray);
      this.set('modal.confirmCallback', callback);
      this.set('modal.isConfirm', true);
    },
    changeSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
    },
    openCreateCategory: function(){
      this.send('closeEditCategory');
      this.set('isCreatingCategory', true);
    },
    closeCreateCategory: function(){
      this.set('errorMessage', '');
      this.set('isCreatingCategory', false);
    },
    createCategory: function(){
      var challengeboard = this.get('selectedChallengeboard');
      var name = this.get('newCategoryName');
      var t =this;

      // error check here
      this.store.filter('category', function(category) {
        return category.get('name') === name;
      }).then(function(foundCategory) {
        var found = foundCategory.get('length');
        if(found){
          t.set('errorMessage', 'Category name already taken');
        } else {
          var category = t.store.createRecord('category', {
            challengeboard: challengeboard,
            name: name,
          });
          category.save().then(function(){
            t.send('closeCreateCategory');
            t.set('newCategoryName', '');
            t.set('errorMessage', '');
          }, function(err){
            category.rollbackAttributes();
            if (err.errors.message){
              t.set('errorMessage', err.errors.message);
            } else {
              t.set('errorMessage', 'Server error, unable to add category');
            }
          });
        }
      });
    },
    openEditCategory: function(category){
      var categoryCopy = {
        id: category.get('id'),
        name: category.get('name'),
      };
      this.send('closeCreateCategory');
      this.set('editingCategory', categoryCopy);
    },
    closeEditCategory: function(){
      this.set('errorMessage', '');
      this.set('editingCategory', null);
    },
    closeEditCategoryDelayed: function(){
      var t = this;
      setTimeout(function(){
        t.set('errorMessage', '');
        t.set('editingCategory', null);
      }, 200);
    },
    editCategory: function(){
      var t = this;
      var newCategory = this.get('editingCategory');
      var category = this.store.peekRecord('category', newCategory.id);

      if(category.get('name') === newCategory.name){
        this.send('closeEditCategory');
        this.set('errorMessage', '');
        return;
      }

      category.set('name', newCategory.name);
      category.save().then(function(){
        t.send('closeEditCategory');
        t.set('errorMessage', '');
      }, function(err){
        category.rollbackAttributes();
        if (err.errors.message){
          t.set('errorMessage', err.errors.message);
        } else {
          t.set('errorMessage', 'Server error, unable to add category');
        }
      });
    },
    deleteCategory: function(category){
      var t = this;
      this.send('promptConfirmation', [
        'This will DELETE the category "' + category.get('name') + '" and all challenges associated with it.',
        'Are you sure?!',
      ], function(confirmed){
        if(confirmed){
          category.deleteRecord();
          category.save().then(function(){
            t.send('closeEditCategory');
            t.set('errorMessage', '');
          }, function(err){
            category.rollbackAttributes();
            if (err.errors.message){
              t.set('errorMessage', err.errors.message);
            } else {
              t.set('errorMessage', 'Server error, unable to delete category');
            }
          });
        }
      });
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
