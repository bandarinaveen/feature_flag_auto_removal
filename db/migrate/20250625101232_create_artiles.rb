class CreateArtiles < ActiveRecord::Migration[7.1]
  def change
    create_table :artiles do |t|
	    t.string "name"
	    t.text "description"
      t.timestamps
    end
  end
end
