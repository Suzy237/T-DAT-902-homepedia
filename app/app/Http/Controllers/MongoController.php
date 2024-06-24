<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use MongoDB\Client as MongoClient;
use MongoDB\Database;
use MongoDB\Collection;
use MongoDB\Exception\Exception;

class MongoController extends Controller
{
    protected $client;
    protected $db;
    protected $safetyCollection;

    public function __construct()
    {
        $this->client = new MongoClient('mongodb://mongo:27017');
        $this->db = $this->client->selectDatabase('housing');
        $this->safetyCollection = $this->db->selectCollection('safety');
    }

    // Function to sanitize input
    protected function sanitizeInput(array $input)
    {
        return array_map(function ($item) {
            return htmlspecialchars(strip_tags($item));
        }, $input);
    }

    // Function to create an index (migration-like)
    public function createIndex()
    {
        try {
            $this->safetyCollection->createIndex(['CODGEO_2023' => 1], ['unique' => true]);
            return response()->json(['status' => 'success', 'message' => 'Index created successfully.']);
        } catch (Exception $e) {
            return response()->json(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }

    // Function to insert safety data
    public function insertSafetyData(Request $request)
    {
        $data = $this->sanitizeInput($request->all());

        try {
            $this->safetyCollection->insertOne($data);
            return response()->json(['status' => 'success', 'message' => 'Data inserted successfully.']);
        } catch (Exception $e) {
            return response()->json(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }

    // Function to get all safety data
    public function getSafetyData()
    {
        try {
            $data = $this->safetyCollection->find()->toArray();
            return response()->json(['status' => 'success', 'data' => $data]);
        } catch (Exception $e) {
            return response()->json(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }

    // Function to update safety data
    public function updateSafetyData(Request $request, $id)
    {
        $data = $this->sanitizeInput($request->all());

        try {
            $this->safetyCollection->updateOne(['_id' => new \MongoDB\BSON\ObjectId($id)], ['$set' => $data]);
            return response()->json(['status' => 'success', 'message' => 'Data updated successfully.']);
        } catch (Exception $e) {
            return response()->json(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }

    // Function to delete safety data
    public function deleteSafetyData($id)
    {
        try {
            $this->safetyCollection->deleteOne(['_id' => new \MongoDB\BSON\ObjectId($id)]);
            return response()->json(['status' => 'success', 'message' => 'Data deleted successfully.']);
        } catch (Exception $e) {
            return response()->json(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }
}
