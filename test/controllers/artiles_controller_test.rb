require "test_helper"

class ArtilesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @artile = artiles(:one)
  end

  test "should get index" do
    get artiles_url
    assert_response :success
  end

  test "should get new" do
    get new_artile_url
    assert_response :success
  end

  test "should create artile" do
    assert_difference("Artile.count") do
      post artiles_url, params: { artile: {  } }
    end

    assert_redirected_to artile_url(Artile.last)
  end

  test "should show artile" do
    get artile_url(@artile)
    assert_response :success
  end

  test "should get edit" do
    get edit_artile_url(@artile)
    assert_response :success
  end

  test "should update artile" do
    patch artile_url(@artile), params: { artile: {  } }
    assert_redirected_to artile_url(@artile)
  end

  test "should destroy artile" do
    assert_difference("Artile.count", -1) do
      delete artile_url(@artile)
    end

    assert_redirected_to artiles_url
  end
end
