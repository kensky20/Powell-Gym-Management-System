<?php

header("Content-Type: application/json");

$host = "localhost";
$dbname = "powell_gym";
$username = "root";
$password = "";

// RESPONSE FUNCTION
function respond($success, $message, $extra = [], $status = 200) {

    http_response_code($status);

    echo json_encode(array_merge([
        "success" => $success,
        "message" => $message
    ], $extra));

    exit;
}

// DATABASE CONNECTION
try {

    $conn = new PDO(
        "mysql:host=$host;dbname=$dbname;charset=utf8mb4",
        $username,
        $password
    );

    $conn->setAttribute(
        PDO::ATTR_ERRMODE,
        PDO::ERRMODE_EXCEPTION
    );

} catch (PDOException $e) {

    respond(false, "Database connection failed.", [], 500);
}

// GET JSON DATA
$data = json_decode(file_get_contents("php://input"), true);

if (!is_array($data)) {
    $data = [];
}

$method = $_SERVER["REQUEST_METHOD"];

// VALIDATION FUNCTION
function validateMember($data) {

    $fields = [
        "full_name",
        "age",
        "gender",
        "contact_number",
        "address",
        "membership_type",
        "start_date",
        "expiration_date"
    ];

    foreach ($fields as $field) {

        if (!isset($data[$field]) ||
            trim((string)$data[$field]) === "") {

            respond(
                false,
                ucfirst(str_replace("_", " ", $field)) . " is required.",
                [],
                400
            );
        }
    }

    // NAME VALIDATION
    $name = trim($data["full_name"]);

    if (!preg_match("/^[\p{L} .'-]+$/u", $name)) {

        respond(false, "Full name must contain letters only.", [], 400);
    }

    // AGE VALIDATION
    $age = filter_var($data["age"], FILTER_VALIDATE_INT);

    if ($age === false || $age < 1 || $age > 120) {

        respond(false, "Age must be between 1 and 120.", [], 400);
    }

    // GENDER VALIDATION
    if (!in_array($data["gender"], ["Male", "Female", "Other"])) {

        respond(false, "Invalid gender.", [], 400);
    }

    // CONTACT VALIDATION
    if (!preg_match("/^(09\d{9}|\+639\d{9})$/",
        trim($data["contact_number"]))) {

        respond(false, "Enter a valid Philippine mobile number.", [], 400);
    }

    // MEMBERSHIP VALIDATION
    $types = [
        "Daily",
        "Weekly",
        "Monthly",
        "Quarterly",
        "Yearly"
    ];

    if (!in_array($data["membership_type"], $types)) {

        respond(false, "Invalid membership type.", [], 400);
    }

    // ADDRESS VALIDATION
    if (strlen(trim($data["address"])) > 255) {

        respond(false, "Address is too long.", [], 400);
    }

    // DATE VALIDATION
    foreach (["start_date", "expiration_date"] as $field) {

        $date = DateTime::createFromFormat("!Y-m-d", $data[$field]);

        if (!$date || $date->format("Y-m-d") !== $data[$field]) {

            respond(false, "Invalid date. Use YYYY-MM-DD.", [], 400);
        }
    }

    if ($data["expiration_date"] < $data["start_date"]) {

        respond(
            false,
            "Expiration date cannot be earlier than start date.",
            [],
            400
        );
    }
}

// MEMBER DATA FUNCTION
function memberValues($data) {

    return [
        trim($data["full_name"]),
        (int)$data["age"],
        $data["gender"],
        trim($data["contact_number"]),
        trim($data["address"]),
        $data["membership_type"],
        $data["start_date"],
        $data["expiration_date"]
    ];
}

try {

    // =================================
    // GET - VIEW AND SEARCH MEMBERS
    // =================================

    if ($method === "GET") {

        $search = trim($_GET["search"] ?? "");

        if ($search !== "") {

            $stmt = $conn->prepare(
                "SELECT * FROM members
                 WHERE CAST(member_id AS CHAR) LIKE ?
                 OR full_name LIKE ?
                 OR contact_number LIKE ?
                 ORDER BY member_id DESC"
            );

            $keyword = "%$search%";

            $stmt->execute([
                $keyword,
                $keyword,
                $keyword
            ]);

        } else {

            $stmt = $conn->query(
                "SELECT * FROM members ORDER BY member_id DESC"
            );
        }

        respond(
            true,
            "Records retrieved successfully.",
            ["members" => $stmt->fetchAll(PDO::FETCH_ASSOC)]
        );
    }

    // =================================
    // POST - ADD MEMBER
    // =================================

    if ($method === "POST") {

        validateMember($data);

        $stmt = $conn->prepare(
            "INSERT INTO members
            (full_name, age, gender, contact_number, address,
            membership_type, start_date, expiration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        );

        $stmt->execute(memberValues($data));

        respond(
            true,
            "Member added successfully.",
            ["member_id" => $conn->lastInsertId()],
            201
        );
    }

    // =================================
    // PUT - UPDATE MEMBER
    // =================================

    if ($method === "PUT") {

        $id = filter_var(
            $_GET["id"] ?? null,
            FILTER_VALIDATE_INT
        );

        if (!$id || $id < 1) {

            respond(false, "Valid member ID is required.", [], 400);
        }

        validateMember($data);

        $check = $conn->prepare(
            "SELECT member_id FROM members WHERE member_id = ?"
        );

        $check->execute([$id]);

        if (!$check->fetch()) {

            respond(false, "Member not found.", [], 404);
        }

        $stmt = $conn->prepare(
            "UPDATE members SET
            full_name = ?,
            age = ?,
            gender = ?,
            contact_number = ?,
            address = ?,
            membership_type = ?,
            start_date = ?,
            expiration_date = ?
            WHERE member_id = ?"
        );

        $values = memberValues($data);
        $values[] = $id;

        $stmt->execute($values);

        respond(true, "Member updated successfully.");
    }

    // =================================
    // DELETE - DELETE MEMBER
    // =================================

    if ($method === "DELETE") {

        $id = filter_var(
            $_GET["id"] ?? null,
            FILTER_VALIDATE_INT
        );

        if (!$id || $id < 1) {

            respond(false, "Valid member ID is required.", [], 400);
        }

        $stmt = $conn->prepare(
            "DELETE FROM members WHERE member_id = ?"
        );

        $stmt->execute([$id]);

        if ($stmt->rowCount() === 0) {

            respond(false, "Member not found.", [], 404);
        }

        respond(true, "Member deleted successfully.");
    }

    respond(false, "Invalid HTTP method.", [], 405);

} catch (PDOException $e) {

    respond(false, "Database operation failed.", [], 500);
}

?>
