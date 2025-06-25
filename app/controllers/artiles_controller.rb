class ArtilesController < ApplicationController
  include ApplicationHelper

  before_action :set_artile, only: %i[ show edit update destroy ]

  # GET /artiles or /artiles.json
  def index
    @flag_name = "pwm-show-articles-list"
    @show_artilces_list = show_feature?("pwm-show-articles-list")
    @artiles = Artile.all
  end

  # GET /artiles/1 or /artiles/1.json
  def show
  end

  # GET /artiles/new
  def new
    @artile = Artile.new
  end

  # GET /artiles/1/edit
  def edit
  end

  # POST /artiles or /artiles.json
  def create
    @artile = Artile.new(artile_params)

    respond_to do |format|
      if @artile.save
        format.html { redirect_to @artile, notice: "Artile was successfully created." }
        format.json { render :show, status: :created, location: @artile }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @artile.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /artiles/1 or /artiles/1.json
  def update
    respond_to do |format|
      if @artile.update(artile_params)
        format.html { redirect_to @artile, notice: "Artile was successfully updated." }
        format.json { render :show, status: :ok, location: @artile }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @artile.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /artiles/1 or /artiles/1.json
  def destroy
    @artile.destroy!

    respond_to do |format|
      format.html { redirect_to artiles_path, status: :see_other, notice: "Artile was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_artile
      @artile = Artile.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def artile_params
      # params.fetch(:artile, {:name, :description})
      params.require(:artile).permit(:name, :description)
    end
end
