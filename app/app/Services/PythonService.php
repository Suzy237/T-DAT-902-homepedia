<?php

namespace App\Services;

use RuntimeException;
use Illuminate\Support\Facades\Log;

class PythonService
{
    protected $pythonScriptPath;

    public function __construct()
    {
        $this->pythonScriptPath = base_path('python_scripts');
    }

    public function runScript($scriptName)
    {
        $scriptPath = $this->pythonScriptPath . '/' . $scriptName;

        Log::info('Executing Python script: ' . $scriptPath);

        $output = [];
        $returnVar = null;
        exec("python3 $scriptPath", $output, $returnVar);

        if ($returnVar !== 0) {
            Log::error('Failed to execute Python script: ', ['output' => $output]);
            throw new RuntimeException('Failed to execute Python script: ' . implode("\n", $output));
        }

        $result = json_decode(implode("\n", $output), true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new RuntimeException('Failed to parse script output: ' . json_last_error_msg());
        }

        return $result;
    }

    public function fetchCsvs()
    {
        return $this->runScript('fetch_csvs.py');
    }

    public function processData()
    {
        return $this->runScript('process_housing_market_data.py');
    }
}
