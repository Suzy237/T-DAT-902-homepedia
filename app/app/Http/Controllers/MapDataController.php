<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class MapDataController extends Controller
{
    public function getDepartments()
    {
        $departments = DB::table('departements')
            ->leftJoin(DB::raw('
                (
                    SELECT DISTINCT ON (LEFT(code_postal, LENGTH(code_postal) - 3)) code_postal, latitude, longitude 
                    FROM cartography 
                    ORDER BY LEFT(code_postal, LENGTH(code_postal) - 3), code_postal
                ) as c'), 'departements.num_dep', '=', DB::raw('LEFT(c.code_postal, LENGTH(departements.num_dep))'))
            ->select('departements.*', 'c.latitude', 'c.longitude')
            ->get();
        return response()->json($departments);
    }

    public function getCities()
    {
        $cities = DB::table('cartography')
            ->select('nom_commune_postal', 'latitude', 'longitude')
            ->get();
        return response()->json($cities);
    }

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
                DB::raw('COUNT(schools.id) as school_count')
            )
            ->groupBy(
                'cartography.nom_commune_postal',
                'cartography.average_cost',
                'cartography.safety_rate'
            )
            ->first();

        return response()->json($location);
    }
}
