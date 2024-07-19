<?php

namespace App\Http\Controllers;

use App\Services\PythonService;
use Illuminate\Support\Facades\Log;
use Illuminate\Http\Request;

class DataController extends Controller
{
    protected $pythonService;

    public function __construct(PythonService $pythonService)
    {
        $this->pythonService = $pythonService;
    }

    public function fetchCsvs()
    {
        try {
            $data = $this->pythonService->fetchCsvs();
            if ($data['status'] !== 'success') {
                return response()->json(['status' => 'error', 'message' => $data['message']], 500);
            }
            return response()->json(['status' => 'success', 'data' => $data['results']]);
        } catch (\Exception $e) {
            Log::error("Error fetching CSVs: " . $e->getMessage());
            return response()->json(['status' => 'error', 'message' => 'Error fetching CSVs'], 500);
        }
    }

    public function processData()
    {
        try {
            $data = $this->pythonService->processData();
            if ($data['status'] !== 'success') {
                return response()->json(['status' => 'error', 'message' => $data['message']], 500);
            }
            return response()->json(['status' => 'success', 'data' => $data['results']]);
        } catch (\Exception $e) {
            Log::error("Error processing data: " . $e->getMessage());
            return response()->json(['status' => 'error', 'message' => 'Error processing data'], 500);
        }
    }
}
