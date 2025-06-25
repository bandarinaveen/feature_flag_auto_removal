require "application_system_test_case"

class ArtilesTest < ApplicationSystemTestCase
  setup do
    @artile = artiles(:one)
  end

  test "visiting the index" do
    visit artiles_url
    assert_selector "h1", text: "Artiles"
  end

  test "should create artile" do
    visit artiles_url
    click_on "New artile"

    click_on "Create Artile"

    assert_text "Artile was successfully created"
    click_on "Back"
  end

  test "should update Artile" do
    visit artile_url(@artile)
    click_on "Edit this artile", match: :first

    click_on "Update Artile"

    assert_text "Artile was successfully updated"
    click_on "Back"
  end

  test "should destroy Artile" do
    visit artile_url(@artile)
    click_on "Destroy this artile", match: :first

    assert_text "Artile was successfully destroyed"
  end
end
