<?php

namespace App\Http\Controllers;

use App\Models\CityData;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class MapDataController extends Controller
{
    public function getLocationDetails($postalCode)
    {
        $location = DB::table('cartography')
            ->leftJoin('real_estate', 'cartography.code_postal', '=', 'real_estate.commune_code')
            ->leftJoin('schools', 'cartography.code_postal', '=', 'schools.postal_code')
            ->leftJoin('safety_data', 'cartography.code_postal', '=', 'safety_data.code_postal')
            ->where('cartography.code_postal', $postalCode)
            ->select(
                'cartography.nom_commune_postal',
                'cartography.average_cost',
                'cartography.safety_rate',
                'cartography.latitude',
                'cartography.longitude',
                DB::raw('COUNT(DISTINCT schools.id) as school_count')
            )
            ->groupBy(
                'cartography.nom_commune_postal',
                'cartography.average_cost',
                'cartography.safety_rate',
                'cartography.latitude',
                'cartography.longitude',
            )
            ->first();

        return response()->json($location);
    }

    public function getCityDataFromMongoDB($postalCode)
    {
        $city = CityData::where('departement', $postalCode)->first();

        return response()->json($city);
    }

    public function findCitiesByName($cityName)
    {
        $cities = DB::table('cartography')
            ->where('nom_commune_postal', 'ilike', '%' . $cityName . '%')
            ->select('nom_commune_postal', 'code_postal', 'latitude', 'longitude', 'average_cost', 'safety_rate')
            ->limit(100)
            ->get();

        return response()->json($cities);
    }
}
