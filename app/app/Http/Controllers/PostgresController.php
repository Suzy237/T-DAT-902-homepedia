<?php

namespace App\Http\Controllers;

use App\Models\RealEstate;
use App\Models\School;
use App\Models\Cartography;
use Illuminate\Http\Request;

class PostgresController extends Controller
{
    public function getRealEstateData()
    {
        return RealEstate::all();
    }

    public function getSchoolData()
    {
        return School::all();
    }

    public function getCartographyData()
    {
        return Cartography::all();
    }
}
