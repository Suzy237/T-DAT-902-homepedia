<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use RuntimeException;
use Illuminate\Support\Facades\Log;

class PythonService
{
    protected $sparkRestUrl;
    protected $maxRetries;
    protected $retryInterval;

    public function __construct()
    {
        $this->sparkRestUrl = env('SPARK_REST_URL', 'http://spark-master:6066');
        $this->maxRetries = env('SPARK_MAX_RETRIES', 10);
        $this->retryInterval = env('SPARK_RETRY_INTERVAL', 10); // in seconds
    }

    public function submitJob($appResource, $args = [], $mainClass = 'org.apache.spark.deploy.PythonRunner')
    {
        $data = [
            'action' => 'CreateSubmissionRequest',
            'appArgs' => $args,
            'appResource' => $appResource,
            'clientSparkVersion' => '3.5.1',
            'mainClass' => $mainClass,
            'environmentVariables' => new \stdClass(),
            'sparkProperties' => [
                'spark.driver.supervise' => 'false',
                'spark.app.name' => 'homepedia',
                'spark.eventLog.enabled' => 'true',
                'spark.submit.deployMode' => 'client',
                'spark.master' => 'spark://spark-master:7077',
                'spark.executor.memory' => '512m',
                'spark.driver.memory' => '512m',
            ]
        ];

        Log::info('Submitting Spark job with data: ', $data);

        $response = Http::post("{$this->sparkRestUrl}/v1/submissions/create", $data);

        if ($response->failed()) {
            Log::error('Failed to submit Spark job: ', ['response' => $response->body()]);
            throw new RuntimeException($response->body());
        }

        $responseData = $response->json();

        if (!isset($responseData['success']) || $responseData['success'] !== true) {
            Log::error('Error in Spark job submission response: ', ['response' => $responseData]);
            throw new RuntimeException("Error submitting job: {$responseData['message']}");
        }

        $submissionId = $responseData['submissionId'];
        return $this->monitorJobStatus($submissionId);
    }


    public function monitorJobStatus($submissionId)
    {
        $statusUrl = "{$this->sparkRestUrl}/v1/submissions/status/$submissionId";
        $retryCount = 0;
        $jobStatus = null;

        while ($retryCount < $this->maxRetries) {
            $response = Http::get($statusUrl);

            if ($response->failed()) {
                Log::error('Failed to get job status: ', ['response' => $response->body()]);
                throw new RuntimeException("Failed to get job status: {$response->body()}");
            }

            $statusData = $response->json();
            $jobStatus = $statusData['driverState'] ?? null;

            Log::info("Job $submissionId status: $jobStatus");

            if ($jobStatus === 'FINISHED') {
                Log::info("Job $submissionId finished successfully.");
                return [
                    'status' => 'success',
                    'message' => 'Job finished successfully',
                    'data' => $statusData
                ];
            } elseif (in_array($jobStatus, ['ERROR', 'FAILED', 'KILLED'])) {
                Log::error("Spark job $submissionId failed with state: $jobStatus");
                throw new RuntimeException("Spark job $submissionId failed with state: $jobStatus");
            }

            sleep($this->retryInterval); // Wait for the configured interval before the next status check
            $retryCount++;
        }

        if ($jobStatus !== 'FINISHED') {
            Log::error("Spark job $submissionId did not finish within the expected time.");
            throw new RuntimeException("Spark job $submissionId did not finish within the expected time.");
        }

        return $statusData;
    }

    public function fetchCsvs()
    {
        return $this->submitJob('hdfs://namenode:8020/python_scripts/fetch_csvs.py', ['hdfs://namenode:8020/python_scripts/fetch_csvs.py']);
    }


    public function processData()
    {
        return $this->submitJob('hdfs://namenode:8020/python_scripts/process_housing_market_data.py', ['hdfs://namenode:8020/python_scripts/process_housing_market_data.py']);
    }
}
